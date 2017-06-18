package com.bigdata.dao.cassandra;



import static com.datastax.spark.connector.japi.CassandraJavaUtil.javaFunctions;
import static com.datastax.spark.connector.japi.CassandraJavaUtil.mapRowTo;
import static com.datastax.spark.connector.japi.CassandraJavaUtil.mapToRow;


import org.apache.spark.api.java.JavaRDD;
import org.apache.spark.api.java.JavaSparkContext;

import com.bigdata.dao.TagDAO;
import com.bigdata.model.Tag;
import com.datastax.driver.core.ConsistencyLevel;
import com.datastax.driver.core.Session;
import com.datastax.spark.connector.cql.CassandraConnector;


public class TagDAOCassandraImpl implements TagDAO {

	private CassandraDAOFactory factory;

	public TagDAOCassandraImpl(CassandraDAOFactory cassandraFactory) {
		this.factory = cassandraFactory;
	}

	@Override
	public JavaRDD<Tag> getAll(JavaSparkContext cxt, Class<Tag> typeClass) {
		String tbl = typeClass.getName().toLowerCase();
		String table = tbl.substring(tbl.lastIndexOf(".")+1)+"s";
		return javaFunctions(cxt).cassandraTable(factory.getKeySpace(), table, mapRowTo(Tag.class))
				.map(f -> {return (Tag) f;});
	}

	@Override
	public void update(JavaRDD<Tag> object) {
		String tbl = Tag.class.getName().toLowerCase();
		String table = tbl.substring(tbl.lastIndexOf(".")+1)+"s";
		javaFunctions(object)
		.writerBuilder(this.factory.getKeySpace(), table, mapToRow(Tag.class))
		.withConsistencyLevel(ConsistencyLevel.LOCAL_ONE)
		.saveToCassandra();
	}
	@Override
	public void remove(JavaRDD<Tag> object) {
		CassandraConnector conn = javaFunctions(object).defaultConnector();
		object.collect().forEach(f-> {
			String tbl = Tag.class.getName().toLowerCase();
			String table = tbl.substring(tbl.lastIndexOf(".")+1)+"s";
			Session session = conn.openSession();
			String query = "DELETE FROM "+factory.getKeySpace()+ "." +table + " WHERE tagid="+f.getTagid();
			session.execute(query);
			session.close();
		});
	}

}
