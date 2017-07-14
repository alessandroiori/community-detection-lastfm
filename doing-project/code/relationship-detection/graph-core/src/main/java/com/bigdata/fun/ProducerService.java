package com.bigdata.fun;

import java.io.Serializable;
import java.util.Properties;

import org.apache.kafka.clients.producer.ProducerRecord;
import org.apache.kafka.common.serialization.StringSerializer;
import org.apache.spark.api.java.JavaRDD;
import org.apache.spark.api.java.JavaSparkContext;

import com.bigdata.dao.DAOFactory;
import com.bigdata.model.Pair;
import com.bigdata.util.customserializer.PairSerializer;
import com.bigdata.util.yaml.Producer;
import com.github.benfradet.spark.kafka010.writer.KafkaWriter;
import com.github.benfradet.spark.kafka010.writer.RDDKafkaWriter;

import scala.Option;
import scala.runtime.AbstractFunction1;

public class ProducerService implements IService, Serializable {

	private static final long serialVersionUID = 1L;
	private FirstPhase first;
	private DAOFactory dao;
	private Properties producerConfig;
	private String topic;

	@Override
	public void run() {
		JavaSparkContext sc = dao.createContext();
		JavaRDD<Pair> rdd = first.run(sc);

		KafkaWriter<Pair> writer = new RDDKafkaWriter<Pair>(rdd.rdd(), 
				scala.reflect.ClassTag$.MODULE$.apply(Pair.class));
		writer.writeToKafka(producerConfig, 
				new SerializableFunc1<Pair, ProducerRecord<String, Pair>>() {
			private static final long serialVersionUID = 1L;

			@Override
			public ProducerRecord<String, Pair> apply(Pair arg0) {
				return new ProducerRecord<String, Pair>(topic, arg0);
			}	
		}, Option.empty());
		sc.close();
	}

	public void setDao(DAOFactory dao) {
		this.dao = dao;
	}

	public void setFirst(FirstPhase first) {
		this.first = first;
	}

	abstract class SerializableFunc1<T, R> extends AbstractFunction1<T, R> implements Serializable {

		private static final long serialVersionUID = 1L;
	}

	public void setProducerConfig(Producer conf) {
		this.producerConfig = new Properties();
		this.topic= conf.getTopic();
		producerConfig.put("bootstrap.servers", conf.getServers());
		producerConfig.put("key.serializer", StringSerializer.class);
		producerConfig.put("value.serializer", PairSerializer.class.getName());
	}

}
