package com.bigdata.dao.cassandra;

import org.apache.spark.SparkConf;
import org.apache.spark.api.java.JavaSparkContext;

import com.bigdata.dao.ArtistDAO;
import com.bigdata.dao.DAOFactory;
import com.bigdata.dao.ListeningDAO;
import com.bigdata.dao.PairDAO;
import com.bigdata.dao.TagAssignementDAO;
import com.bigdata.dao.TagDAO;
import com.bigdata.dao.UserDAO;
import com.bigdata.main.MyContext;
import com.bigdata.util.yaml.Cassandra;

public class CassandraDAOFactory extends DAOFactory {

	/**
	 * 
	 */
	private static final long serialVersionUID = 1L;
	private Cassandra conf;

	@Override
	public UserDAO getUserDAO() {
		return new UserDAOCassandraImpl(this);
	}

	@Override
	public ArtistDAO getArtistDAO() {
		return new ArtistDAOCassandraImpl(this);
	}

	@Override
	public TagDAO getTagDAO() {
		return new TagDAOCassandraImpl(this);
	}

	@Override
	public ListeningDAO getListeningDAO() {
		return new ListeningDAOCassandraImpl(this);
	}

	@Override
	public TagAssignementDAO getTagAssignementDAO() {

		return new TagAssignementDAOCassandraImpl(this);
	}
	
	@Override
	public PairDAO getPairDAO() {
		return new PairDAOCassandraImpl(this);
	}
	
	public void setConfiguration(Cassandra conf)  {
		this.conf = conf;
	}
	
	protected String getKeySpace() {
		return this.conf.getKeyspace();
	}

	@Override
	public JavaSparkContext createContext() {
		SparkConf config = new SparkConf();
        config.setAppName(MyContext.APP_NAME);
        config.setMaster(conf.master);
        config.set("spark.cassandra.connection.host", conf.host);
        return new JavaSparkContext(config);
	}
	
}