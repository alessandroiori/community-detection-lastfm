package com.bigdata.dao.cassandra;


import static com.datastax.spark.connector.japi.CassandraJavaUtil.javaFunctions;
import static com.datastax.spark.connector.japi.CassandraJavaUtil.mapRowTo;
import static com.datastax.spark.connector.japi.CassandraJavaUtil.mapToRow;
import org.apache.spark.api.java.JavaRDD;
import org.apache.spark.api.java.JavaSparkContext;

import com.bigdata.dao.TagAssignementDAO;
import com.bigdata.model.TagAssignement;
import com.datastax.driver.core.ConsistencyLevel;
import com.datastax.spark.connector.cql.CassandraConnector;
import com.datastax.spark.connector.japi.CassandraJavaUtil;
import com.datastax.spark.connector.japi.RDDJavaFunctions;
import com.datastax.spark.connector.writer.WriteConf;

public class TagAssignementDAOCassandraImpl implements TagAssignementDAO {

	/**
	 * 
	 */
	private static final long serialVersionUID = 1L;
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
	RDDJavaFunctions<TagAssignement> functions = javaFunctions(object);
	CassandraConnector conn = functions.defaultConnector();
	WriteConf wconf = functions.
			writerBuilder(this.factory.getKeySpace(), table, mapToRow(TagAssignement.class))
			.withConsistencyLevel(ConsistencyLevel.LOCAL_ONE).writeConf;
	functions.deleteFromCassandra(factory.getKeySpace(), table, 
			mapToRow(TagAssignement.class), CassandraJavaUtil.someColumns(), 
			CassandraJavaUtil.someColumns("userid"), wconf, conn);
}

}
