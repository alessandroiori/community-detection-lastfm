package com.bigdata.main;

import java.io.IOException;
import java.io.InputStream;
import java.nio.file.Files;
import java.nio.file.Paths;

import org.yaml.snakeyaml.Yaml;

import com.bigdata.dao.cassandra.CassandraDAOFactory;
import com.bigdata.fun.Similarity;
import com.bigdata.fun.TemplateMethod;
import com.bigdata.yaml.Cassandra;
import com.bigdata.yaml.Configuration;

public class MyContext {
	//private final static String FUNCTION_PACKAGE="com.bigdata.fun.";
	private final static String YAML_FILE="application.yml";
	//private final static String DAO="com.bigdata.dao.GenericDAO";

	private static MyContext instance = null;
	private Configuration conf = null;


	public static synchronized MyContext getInstance() {
		if (instance == null) 
			instance = new MyContext();
		return instance;
	}

	public TemplateMethod getSimilarity(Double thres) {
		Configuration config = getConfiguration();

		CassandraDAOFactory factory = new CassandraDAOFactory();
		factory.setConfiguration(config.getCassandra());
		Similarity sim =  new Similarity();
		sim.setThreshould(thres);

		TemplateMethod method = new TemplateMethod();
		method.setFirst(sim);
		method.setSecond(sim);
		method.setInput(factory);
		method.setOutput(factory);
		return method;
	}

	private Configuration getConfiguration() {
		if (conf == null) {
			Yaml yaml = new Yaml();  
			try( InputStream in = Files.newInputStream(Paths.get(YAML_FILE))) {
				conf = yaml.loadAs( in, Configuration.class );
				System.out.println( conf.toString() );
			} catch (IOException e) {
				e.printStackTrace();
			}
		}
		return conf;
	}

}
