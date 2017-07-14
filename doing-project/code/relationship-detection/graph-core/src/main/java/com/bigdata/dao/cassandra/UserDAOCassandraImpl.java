package com.bigdata.dao.cassandra;


import static com.datastax.spark.connector.japi.CassandraJavaUtil.javaFunctions;
import static com.datastax.spark.connector.japi.CassandraJavaUtil.mapRowTo;
import static com.datastax.spark.connector.japi.CassandraJavaUtil.mapToRow;

import org.apache.spark.api.java.JavaRDD;
import org.apache.spark.api.java.JavaSparkContext;

import com.bigdata.dao.UserDAO;
import com.bigdata.model.User;
import com.datastax.driver.core.ConsistencyLevel;
import com.datastax.spark.connector.cql.CassandraConnector;
import com.datastax.spark.connector.japi.CassandraJavaUtil;
import com.datastax.spark.connector.japi.RDDJavaFunctions;
import com.datastax.spark.connector.writer.WriteConf;

public class UserDAOCassandraImpl implements UserDAO {

	/**
	 * 
	 */
	private static final long serialVersionUID = 1L;
	private CassandraDAOFactory factory;

	public UserDAOCassandraImpl(CassandraDAOFactory cassandraFactory) {
		this.factory = cassandraFactory;
	}

	@Override
	public JavaRDD<User> getAll(JavaSparkContext cxt, Class<User> typeClass) {
		String tbl = typeClass.getName().toLowerCase();
		String table = tbl.substring(tbl.lastIndexOf(".")+1)+"s";
		return javaFunctions(cxt).cassandraTable(factory.getKeySpace(), table, mapRowTo(User.class))
				.map(f -> {return (User) f;});
	}

	@Override
	public void update(JavaRDD<User> object) {
		String tbl = User.class.getName().toLowerCase();
		String table = tbl.substring(tbl.lastIndexOf(".")+1)+"s";
		javaFunctions(object)
		.writerBuilder(this.factory.getKeySpace(), table, mapToRow(User.class))
		.withConsistencyLevel(ConsistencyLevel.LOCAL_ONE)
		.saveToCassandra();
	}
	@Override
	public void remove(JavaRDD<User> object) {
		String tbl = User.class.getName().toLowerCase();
		String table = tbl.substring(tbl.lastIndexOf(".")+1)+"s";
		RDDJavaFunctions<User> functions = javaFunctions(object);
		CassandraConnector conn = functions.defaultConnector();
		WriteConf wconf = functions.
				writerBuilder(this.factory.getKeySpace(), table, mapToRow(User.class))
				.withConsistencyLevel(ConsistencyLevel.LOCAL_ONE).writeConf;
		functions.deleteFromCassandra(factory.getKeySpace(), table, 
				mapToRow(User.class), CassandraJavaUtil.someColumns(), 
				CassandraJavaUtil.someColumns("userid"), wconf, conn);
	}
}
