package com.bigdata.dao.cassandra;

import static com.datastax.spark.connector.japi.CassandraJavaUtil.*;
import org.apache.spark.api.java.JavaRDD;
import org.apache.spark.api.java.JavaSparkContext;

import com.bigdata.dao.ListeningDAO;
import com.bigdata.model.Listening;
import com.datastax.driver.core.ConsistencyLevel;
import com.datastax.spark.connector.cql.CassandraConnector;
import com.datastax.spark.connector.japi.CassandraJavaUtil;
import com.datastax.spark.connector.japi.RDDJavaFunctions;
import com.datastax.spark.connector.writer.WriteConf;


public class ListeningDAOCassandraImpl implements ListeningDAO {

	/**
	 * 
	 */
	private static final long serialVersionUID = 1L;
	private CassandraDAOFactory factory;

	public ListeningDAOCassandraImpl(CassandraDAOFactory cassandraFactory) {
		this.factory = cassandraFactory;
	}

	@Override
	public JavaRDD<Listening> getAll(JavaSparkContext cxt, Class<Listening> typeClass) {
		String tbl = typeClass.getName().toLowerCase();
		String table = tbl.substring(tbl.lastIndexOf(".")+1)+"s";
		return javaFunctions(cxt)
				.cassandraTable(factory.getKeySpace(), table, mapRowTo(Listening.class))
				.map(f -> {return (Listening) f;});
	}

	@Override
	public void update(JavaRDD<Listening> object) {
		String tbl = Listening.class.getName().toLowerCase();
		String table = tbl.substring(tbl.lastIndexOf(".")+1)+"s";
		javaFunctions(object)
		.writerBuilder(this.factory.getKeySpace(), table, mapToRow(Listening.class))
		.withConsistencyLevel(ConsistencyLevel.LOCAL_ONE)
		.saveToCassandra();
	}


	@Override
	public void remove(JavaRDD<Listening> object) {
		String tbl = Listening.class.getName().toLowerCase();
		String table = tbl.substring(tbl.lastIndexOf(".")+1)+"s";

		RDDJavaFunctions<Listening> functions = javaFunctions(object);
		CassandraConnector conn = functions.defaultConnector();
		WriteConf wconf = functions.
				writerBuilder(this.factory.getKeySpace(), table, mapToRow(Listening.class))
				.withConsistencyLevel(ConsistencyLevel.LOCAL_ONE).writeConf;
		functions.deleteFromCassandra(factory.getKeySpace(), table, 
				mapToRow(Listening.class), CassandraJavaUtil.someColumns(), 
				CassandraJavaUtil.someColumns("userid"), wconf, conn);
	}
}
