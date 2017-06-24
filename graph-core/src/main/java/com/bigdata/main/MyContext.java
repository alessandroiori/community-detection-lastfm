package com.bigdata.main;

import java.io.IOException;
import java.io.InputStream;
import java.nio.file.Files;
import java.nio.file.Paths;

import org.yaml.snakeyaml.Yaml;

import com.bigdata.dao.DAOFactory;
import com.bigdata.dao.cassandra.CassandraDAOFactory;
import com.bigdata.fun.Similarity;
import com.bigdata.fun.ConsumerService;
import com.bigdata.fun.IService;
import com.bigdata.fun.ProducerService;
import com.bigdata.fun.SingleService;
import com.bigdata.util.yaml.Configuration;
public class MyContext {
	private String yaml_file;
	private final static String SINGLE_SERVICE = "single";
	private final static String PRODUCER_SERVICE = "producer";
	private final static String CONSUMER_SERVICE = "consumer";
	public static final String APP_NAME = "graph-core";

	private static MyContext instance = null;
	private Configuration conf = null;


	public static synchronized MyContext getInstance() {
		if (instance == null) 
			instance = new MyContext();
		return instance;
	}

	public IService getService(String yml, Double thres) {
		this.yaml_file = yml;
		Configuration config = getConfiguration();
		IService service = null;
		switch (config.getService()) {
		case SINGLE_SERVICE:
			service = getSingleService(thres);
			break;
		case PRODUCER_SERVICE:
			service = getProducerService(thres);
			break;
		case CONSUMER_SERVICE:
			service = getConsumerService(thres);
			break;
		default:
			service = getSingleService(thres);
			break;
		}
		return service;
	}

	private IService getProducerService(Double thres) {
		DAOFactory factory = getInputFactory();
		Similarity sim =  new Similarity();
		sim.setThreshould(thres);

		ProducerService method = new ProducerService();
		method.setFirst(sim);
		method.setDao(factory);
		method.setProducerConfig(this.getConfiguration().getProducer());
		return (IService) method;
	}
	
	private IService getConsumerService(Double thres) {
		DAOFactory factory = getInputFactory();
		Similarity sim =  new Similarity();
		sim.setThreshould(thres);

		ConsumerService method = new ConsumerService();
		method.setSecond(sim);
		method.setDao(factory);
		method.setConsumerConfig(this.getConfiguration().getConsumer());
		return (IService) method;
	}

	private DAOFactory getInputFactory() {
		CassandraDAOFactory factory = new CassandraDAOFactory();
		factory.setConfiguration(this.getConfiguration().getCassandra());
		return factory;
	}
	
	private DAOFactory getOutputFactory() {
		CassandraDAOFactory factory = new CassandraDAOFactory();
		factory.setConfiguration(this.getConfiguration().getCassandra());
		return factory;
	}
	
	private IService getSingleService(Double thres) {
		DAOFactory in = getInputFactory();
		DAOFactory out = getOutputFactory();
		Similarity sim =  new Similarity();
		sim.setThreshould(thres);

		SingleService method = new SingleService();
		method.setFirst(sim);
		method.setSecond(sim);
		method.setInput(in);
		method.setOutput(out);
		return (IService) method;
	}

	private Configuration getConfiguration() {
		if (conf == null) {
			Yaml yaml = new Yaml();  
			try( InputStream in = Files.newInputStream(Paths.get(yaml_file))) {
				conf = yaml.loadAs( in, Configuration.class );
				System.out.println( conf.toString() );
			} catch (IOException e) {
				e.printStackTrace();
			}
		}
		return conf;
	}

}
