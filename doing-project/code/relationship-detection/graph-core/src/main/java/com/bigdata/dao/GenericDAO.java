package com.bigdata.dao;

import java.io.Serializable;

import org.apache.spark.api.java.JavaRDD;
import org.apache.spark.api.java.JavaSparkContext;


public interface GenericDAO <T, K extends Serializable> extends Serializable {  

	JavaRDD<T> getAll(JavaSparkContext cxt, Class<T> typeClass);   
	void update(JavaRDD<T> object);
	//TODO - void insert(T object);  
	void remove(JavaRDD<T> object);
}

