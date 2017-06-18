package com.bigdata.yaml;
public final class Configuration { 

	private Cassandra cassandra;

	public Cassandra getCassandra() {
		return cassandra;
	}

	public void setCassandra(Cassandra cassandraConfiguration) {
		this.cassandra = cassandraConfiguration;
	}
	
    @Override
    public String toString() {
    	return cassandra.toString();
    }
}