package com.bigdata.dao.cassandra;

import static com.datastax.spark.connector.japi.CassandraJavaUtil.javaFunctions;
import static com.datastax.spark.connector.japi.CassandraJavaUtil.mapRowTo;
import static com.datastax.spark.connector.japi.CassandraJavaUtil.mapToRow;

import org.apache.spark.api.java.JavaRDD;
import org.apache.spark.api.java.JavaSparkContext;

import com.bigdata.dao.PairDAO;
import com.bigdata.model.Pair;
import com.datastax.driver.core.ConsistencyLevel;
import com.datastax.driver.core.Session;
import com.datastax.spark.connector.cql.CassandraConnector;

public class PairDAOCassandraImpl implements PairDAO {

	/**
	 * 
	 */
	private static final long serialVersionUID = 1L;
	private CassandraDAOFactory factory;

	public PairDAOCassandraImpl(CassandraDAOFactory cassandraFactory) {
		this.factory = cassandraFactory;
	}

	
	@Override
	public JavaRDD<Pair> getAll(JavaSparkContext cxt, Class<Pair> typeClass) {
		String tbl = typeClass.getName().toLowerCase();
		String table = tbl.substring(tbl.lastIndexOf(".")+1)+"s";
		return javaFunctions(cxt)
				.cassandraTable(factory.getKeySpace(), table, mapRowTo(Pair.class))
				.map(f -> {return (Pair) f;});
	}

	@Override
	public void update(JavaRDD<Pair> object) {
		String tbl = Pair.class.getName().toLowerCase();
		String table = tbl.substring(tbl.lastIndexOf(".")+1)+"s";
		javaFunctions(object)
		.writerBuilder(this.factory.getKeySpace(), table, mapToRow(Pair.class))
		.withConsistencyLevel(ConsistencyLevel.LOCAL_ONE)
		.saveToCassandra();
	}

	@Override
	public void remove(JavaRDD<Pair> object) {
		String tbl = Pair.class.getName().toLowerCase();
		String table = tbl.substring(tbl.lastIndexOf(".")+1)+"s";
		CassandraConnector conn = javaFunctions(object).defaultConnector();
		object.collect().forEach(f-> {
			Session session = conn.openSession();
			String query = "DELETE FROM "+factory.getKeySpace()+ "." +table + 
					" WHERE id1="+f.getId1()+ " and id2="+f.getId2();
			session.execute(query);
			session.close();
		});
	}

}
