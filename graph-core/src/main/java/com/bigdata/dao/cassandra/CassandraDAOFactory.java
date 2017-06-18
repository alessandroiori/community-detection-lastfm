package com.bigdata.dao.cassandra;

import org.apache.spark.SparkConf;
import org.apache.spark.api.java.JavaSparkContext;
import org.apache.spark.sql.SQLContext;

import com.bigdata.dao.ArtistDAO;
import com.bigdata.dao.DAOFactory;
import com.bigdata.dao.ListeningDAO;
import com.bigdata.dao.TagAssignementDAO;
import com.bigdata.dao.TagDAO;
import com.bigdata.dao.UserDAO;
import com.bigdata.yaml.CassandraConfig;

public class CassandraDAOFactory extends DAOFactory {

	private CassandraConfig conf;

	@Override
	public UserDAO getUserDAO() {
		UserDAO DAO = (UserDAO) new UserDAOCassandraImpl(this);
		return DAO;
	}

	@Override
	public ArtistDAO getArtistDAO() {
		ArtistDAO DAO = (ArtistDAO) new ArtistDAOCassandraImpl(this);
		return DAO;
	}

	@Override
	public TagDAO getTagDAO() {
		TagDAO DAO = (TagDAO) new TagDAOCassandraImpl(this);
		return DAO;
	}

	@Override
	public ListeningDAO getListeningDAO() {
		ListeningDAO DAO = (ListeningDAO) new ListeningDAOCassandraImpl(this);
		return DAO;
	}

	@Override
	public TagAssignementDAO getTagAssignementDAO() {
		TagAssignementDAO DAO = (TagAssignementDAO) new TagAssignementDAOCassandraImpl(this);
		return DAO;
	}
	
	public void setConfiguration(CassandraConfig conf)  {
		this.conf = conf;
	}
	
	protected String getKeySpace() {
		return this.conf.keySpace;
	}

	@Override
	public JavaSparkContext createContext() {
		SparkConf config = new SparkConf();
        config.setAppName("Java API demo");
        config.setMaster(conf.master);
        config.set("spark.cassandra.connection.host", conf.host);
        return new JavaSparkContext(config);
	}
	
}