package com.bigdata.dao.cassandra;

import static com.datastax.spark.connector.japi.CassandraJavaUtil.javaFunctions;
import static com.datastax.spark.connector.japi.CassandraJavaUtil.mapRowTo;
import static com.datastax.spark.connector.japi.CassandraJavaUtil.mapToRow;

import org.apache.spark.api.java.JavaRDD;
import org.apache.spark.api.java.JavaSparkContext;

import com.bigdata.dao.ArtistDAO;
import com.bigdata.model.Artist;
import com.datastax.driver.core.ConsistencyLevel;
import com.datastax.driver.core.Session;
import com.datastax.spark.connector.cql.CassandraConnector;

public class ArtistDAOCassandraImpl implements ArtistDAO {

	private CassandraDAOFactory factory;

	public ArtistDAOCassandraImpl(CassandraDAOFactory cassandraFactory) {
		this.factory = cassandraFactory;
	}

	@Override
	public JavaRDD<Artist> getAll(JavaSparkContext cxt, Class<Artist> typeClass) {
		String tbl = typeClass.getName().toLowerCase();
		String table = tbl.substring(tbl.lastIndexOf(".")+1)+"s";
		return javaFunctions(cxt).cassandraTable(factory.getKeySpace(), table, mapRowTo(Artist.class))
				.map(f -> {return (Artist) f;});
	}

	@Override
	public void update(JavaRDD<Artist> object) {
		String tbl = Artist.class.getName().toLowerCase();
		String table = tbl.substring(tbl.lastIndexOf(".")+1)+"s";
		javaFunctions(object)
		.writerBuilder(this.factory.getKeySpace(), table, mapToRow(Artist.class))
		.withConsistencyLevel(ConsistencyLevel.LOCAL_ONE)
		.saveToCassandra();
	}

	@Override
	public void remove(JavaRDD<Artist> object) {
		String tbl = Artist.class.getName().toLowerCase();
		String table = tbl.substring(tbl.lastIndexOf(".")+1)+"s";
		CassandraConnector conn = javaFunctions(object).defaultConnector();
		object.collect().forEach(f-> {
			Session session = conn.openSession();
			String query = "DELETE FROM "+factory.getKeySpace()+ "." +table + " WHERE artistid="+f.getArtistid();
			session.execute(query);
			session.close();
		});
	}


}
