package com.bigdata.fun;


import java.util.HashMap;

import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.apache.kafka.common.serialization.StringDeserializer;
import org.apache.spark.api.java.JavaRDD;
import org.apache.spark.api.java.JavaSparkContext;
import org.apache.spark.streaming.kafka010.KafkaUtils;
import org.apache.spark.streaming.kafka010.LocationStrategies;
import org.apache.spark.streaming.kafka010.OffsetRange;

import com.bigdata.dao.DAOFactory;
import com.bigdata.model.Pair;
import com.bigdata.util.customserializer.PairDeserializer;
import com.bigdata.util.yaml.Consumer;


public class ConsumerService implements IService {

	private DAOFactory dao;
	private SecondPhase second;
	private String topic;
	private HashMap<String, Object> kafkaParams;
	

	@Override
	public void run() {
		JavaSparkContext sc = dao.createContext();
		
		//TODO - get latest offsets
		OffsetRange[] offsetRanges = {
				// topic, partition, inclusive starting offset, exclusive ending offset
				OffsetRange.create(this.topic, 0, 0, 1076)
		};
		
		JavaRDD<ConsumerRecord<String, Pair>> rdd = KafkaUtils.createRDD(
				sc, 
				kafkaParams, 
				offsetRanges, 
				LocationStrategies.PreferConsistent());
		
		JavaRDD<Pair> clenedRDD = rdd.map(f-> {
			return f.value();
		});
		
		
		
		second.run(clenedRDD);
		

		dao.getPairDAO().update(newRDD);
		
		sc.stop();
		sc.close();
	}


	public void setDao(DAOFactory dao) {
		this.dao = dao;
	}


	public SecondPhase getSecond() {
		return second;
	}


	public void setSecond(SecondPhase second) {
		this.second = second;
	}

	public void setConsumerConfig(Consumer conf) {
		this.topic= conf.getTopic();
		this.kafkaParams = new HashMap<String, Object>();
		kafkaParams.put("bootstrap.servers", "localhost:9092");
		kafkaParams.put("key.deserializer", StringDeserializer.class);
		kafkaParams.put("value.deserializer", PairDeserializer.class.getName());
	}


}
