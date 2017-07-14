package com.bigdata.model;

import java.io.Serializable;

public class Listening implements Serializable {
	
	/**
	 * 
	 */
	private static final long serialVersionUID = 1L;

	private Long userID;
	
	private Long artistID;
	
	private Long listenings;

	public Long getUserid() {
		return userID;
	}

	public void setUserid(Long userId) {
		this.userID = userId;
	}

	public Long getArtistid() {
		return artistID;
	}

	public void setArtistid(Long artistId) {
		this.artistID = artistId;
	}

	public Long getListenings() {
		return listenings;
	}

	public void setListenings(Long listenings) {
		this.listenings = listenings;
	}
	
	@Override
	public String toString() {
		return this.userID + "\t" + this.artistID + "\t" + this.listenings;
	}
	
}
