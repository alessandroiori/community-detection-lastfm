package com.bigdata.fun;

import org.apache.spark.api.java.JavaRDD;

import com.bigdata.dao.DAOFactory;
import com.bigdata.model.Pair;

public interface SecondPhase {

	public void run(JavaRDD<Pair> rdd);
}
