package com.bigdata.fun;

import org.apache.spark.api.java.JavaRDD;
import org.apache.spark.api.java.JavaSparkContext;

import com.bigdata.model.Pair;

public interface FirstPhase {
	
	public JavaRDD<Pair> run(JavaSparkContext scIn);

	
}
