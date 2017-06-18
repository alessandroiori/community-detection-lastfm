package com.bigdata.main;

import com.bigdata.dao.cassandra.CassandraDAOFactory;
import com.bigdata.fun.Function;
import com.bigdata.fun.Similarity;
import com.bigdata.yaml.CassandraConfig;

public class MyContext {
	//private final static String FUNCTION_PACKAGE="com.bigdata.fun.";
	//private final static String YAML_FILE="../application.yml";
	//private final static String DAO="com.bigdata.dao.GenericDAO";

	private static MyContext instance = null;
	
	public static synchronized MyContext getInstance() {
		if (instance == null) 
			instance = new MyContext();
		return instance;
	}

	public Function getSimilarity(Double thres) {
		CassandraDAOFactory factory = new CassandraDAOFactory();
		CassandraConfig cn = new CassandraConfig();
		cn.host = "localhost";
		cn.master = "local[1]";
		cn.keySpace = "lastfm";
		factory.setConfiguration(cn);
		Similarity sim =  new Similarity();
		sim.setThreshould(thres);
		sim.setInputDAOFactory(factory);
			
		return sim;
	}

}
