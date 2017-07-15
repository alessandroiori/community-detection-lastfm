package com.bigdata.dao.cassandra;

import static com.datastax.spark.connector.japi.CassandraJavaUtil.javaFunctions;
import static com.datastax.spark.connector.japi.CassandraJavaUtil.mapRowTo;
import static com.datastax.spark.connector.japi.CassandraJavaUtil.mapToRow;

import org.apache.spark.api.java.JavaRDD;
import org.apache.spark.api.java.JavaSparkContext;

import com.bigdata.dao.PairDAO;
import com.bigdata.model.Pair;
import com.datastax.driver.core.ConsistencyLevel;
import com.datastax.spark.connector.cql.CassandraConnector;
import com.datastax.spark.connector.japi.CassandraJavaUtil;
import com.datastax.spark.connector.japi.RDDJavaFunctions;
import com.datastax.spark.connector.writer.WriteConf;

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
		RDDJavaFunctions<Pair> functions = javaFunctions(object);
		CassandraConnector conn = functions.defaultConnector();
		WriteConf wconf = functions.
				writerBuilder(this.factory.getKeySpace(), table, mapToRow(Pair.class))
				.withConsistencyLevel(ConsistencyLevel.LOCAL_ONE).writeConf;
		functions.deleteFromCassandra(factory.getKeySpace(), table, 
				mapToRow(Pair.class), CassandraJavaUtil.someColumns(), 
				CassandraJavaUtil.someColumns("id1"), wconf, conn);
	}

}
