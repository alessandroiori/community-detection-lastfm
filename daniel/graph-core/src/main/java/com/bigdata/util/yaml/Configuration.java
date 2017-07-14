package com.bigdata.util.yaml;
public final class Configuration { 
	
	
	private String service;
	private Cassandra cassandra;
	private Producer producer;
	private Consumer consumer;
	
	public Cassandra getCassandra() {
		return cassandra;
	}

	public void setCassandra(Cassandra cassandraConfiguration) {
		this.cassandra = cassandraConfiguration;
	}
	
	public String getService() {
		return service;
	}

	public void setService(String service) {
		this.service = service;
	}

	public Producer getProducer() {
		return producer;
	}

	public void setProducer(Producer producer) {
		this.producer = producer;
	}

	public Consumer getConsumer() {
		return consumer;
	}

	public void setConsumer(Consumer consumer) {
		this.consumer = consumer;
	}
	
	@Override
	public String toString() {
		return "Service:\t"+ this.service + "\n" + cassandra.toString();
	}
}