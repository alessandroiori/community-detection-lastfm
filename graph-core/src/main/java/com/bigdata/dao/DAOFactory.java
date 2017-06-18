package com.bigdata.dao;

import java.io.Serializable;

import org.apache.spark.api.java.JavaSparkContext;

public abstract class DAOFactory implements Serializable{

	private static final long serialVersionUID = 1L;
	public abstract UserDAO getUserDAO();
	public abstract ArtistDAO getArtistDAO();
	public abstract TagDAO getTagDAO();
	public abstract ListeningDAO getListeningDAO();
	public abstract TagAssignementDAO getTagAssignementDAO();
	
	public abstract JavaSparkContext createContext();
	
}
