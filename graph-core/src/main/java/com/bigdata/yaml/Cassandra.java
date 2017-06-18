package com.bigdata.yaml;

import java.io.Serializable;

public class Cassandra  implements Serializable {
	
	/**
	 * 
	 */
	private static final long serialVersionUID = 1L;
	public String keyspace;
	public String master;
	public String host;
	
	public String getKeyspace() {
		return keyspace;
	}
	public void setKeyspace(String keySpace) {
		this.keyspace = keySpace;
	}
	public String getMaster() {
		return master;
	}
	
	public String getHost() {
		return host;
	}
	
	public void setHost(String host) {
		this.host = host;
	}
	
	public void setMaster(String master) {
		this.master = master;
	}
	
	@Override
	public String toString() {
		StringBuilder builder = new StringBuilder();
		builder.append("Cassandra configuration: ");
		builder.append("\n\tHost: "+host);
		builder.append("\n\tMaster: "+master);
		builder.append("\n\tKey space: "+keyspace);
		
		return builder.toString();
	}
}
