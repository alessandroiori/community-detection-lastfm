package com.bigdata.util.customserializer;

import java.util.Map;

import org.apache.kafka.common.serialization.Deserializer;

import com.bigdata.model.Pair;
import com.fasterxml.jackson.databind.ObjectMapper;

public class PairDeserializer implements Deserializer<Pair> {

	@Override
	public void close() {

	}

	@Override
	public void configure(Map<String, ?> arg0, boolean arg1) {

	}

	@Override
	public Pair deserialize(String arg0, byte[] arg1) {
		ObjectMapper mapper = new ObjectMapper();
		Pair pair = null;
		try {
			pair = mapper.readValue(arg1, Pair.class);
		} catch (Exception e) {

			e.printStackTrace();
		}
		return pair;
	}

}
