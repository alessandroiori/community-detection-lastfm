package com.bigdata.fun;

import org.apache.spark.api.java.JavaRDD;

import com.bigdata.model.Pair;

public interface SecondPhase {

	public JavaRDD<Pair> run(JavaRDD<Pair> rdd);
}
