package com.bigdata.dao.cassandra;


import static com.datastax.spark.connector.japi.CassandraJavaUtil.javaFunctions;
import static com.datastax.spark.connector.japi.CassandraJavaUtil.mapRowTo;
import static com.datastax.spark.connector.japi.CassandraJavaUtil.mapToRow;

import org.apache.spark.api.java.JavaRDD;
import org.apache.spark.api.java.JavaSparkContext;

import com.bigdata.dao.TagAssignementDAO;
import com.bigdata.model.TagAssignement;
import com.datastax.driver.core.ConsistencyLevel;
import com.datastax.driver.core.Session;
import com.datastax.spark.connector.cql.CassandraConnector;

public class TagAssignementDAOCassandraImpl implements TagAssignementDAO {

	private CassandraDAOFactory factory;

	public TagAssignementDAOCassandraImpl(CassandraDAOFactory cassandraFactory) {
		this.factory = cassandraFactory;
	}

	@Override
	public JavaRDD<TagAssignement> getAll(JavaSparkContext cxt, Class<TagAssignement> typeClass) {
		String tbl = typeClass.getName().toLowerCase();
		String table = tbl.substring(tbl.lastIndexOf(".")+1)+"s";
		return javaFunctions(cxt).cassandraTable(factory.getKeySpace(), table, mapRowTo(TagAssignement.class))
				.map(f -> {return (TagAssignement) f;});
	}

	@Override
	public void update(JavaRDD<TagAssignement> object) {
		String tbl = TagAssignement.class.getName().toLowerCase();
		String table = tbl.substring(tbl.lastIndexOf(".")+1)+"s";
		javaFunctions(object)
		.writerBuilder(this.factory.getKeySpace(), table, mapToRow(TagAssignement.class))
		.withConsistencyLevel(ConsistencyLevel.LOCAL_ONE)
		.saveToCassandra();
	}
	
@Override
public void remove(JavaRDD<TagAssignement> object) {
	String tbl = TagAssignement.class.getName().toLowerCase();
	String table = tbl.substring(tbl.lastIndexOf(".")+1)+"s";
	CassandraConnector conn = javaFunctions(object).defaultConnector();
	object.collect().forEach(f-> {
		Session session = conn.openSession();
		String query = "DELETE FROM "+factory.getKeySpace()+ "." +table +
				" WHERE artistid="+f.getArtistid()+" and userid="+f.getUserid() + "and tagid=" +f.getTagid();
		session.execute(query);
		session.close();
	});
}

}
