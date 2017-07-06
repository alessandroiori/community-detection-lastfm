package com.bigdata.util.customserializer;

import java.util.Map;

import org.apache.kafka.common.serialization.Serializer;

import com.bigdata.model.Pair;
import com.fasterxml.jackson.databind.ObjectMapper;

public class PairSerializer  implements Serializer<Pair> {
	 
	  @Override
	  public void close() {
	 
	  }
	 
	  @Override
	  public void configure(Map<String, ?> arg0, boolean arg1) {
	 
	  }
	 
	  @Override
	  public byte[] serialize(String arg0, Pair arg1) {
	    byte[] retVal = null;
	    ObjectMapper objectMapper = new ObjectMapper();
	    try {
	      retVal = objectMapper.writeValueAsString(arg1).getBytes();
	    } catch (Exception e) {
	      e.printStackTrace();
	    }
	    return retVal;
	  }

}
