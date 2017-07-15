package com.bigdata.model;

import java.io.Serializable;

public class Artist implements Serializable {

	/**
	 * 
	 */
	private static final long serialVersionUID = 1L;

	private Long artistId;
	
	private String artistName;
    
	private String pictureUrl;
    
	private String url;
	
	
	public Long getArtistid() {
		return artistId;
	}

	public void setArtistid(Long artistId) {
		this.artistId = artistId;
	}

	public String getArtistname() {
		return artistName;
	}

	public void setArtistname(String artistName) {
		this.artistName = artistName;
	}

	public String getArtistpictureurl() {
		return pictureUrl;
	}

	public void setArtistpictureurl(String pictureUrl) {
		this.pictureUrl = pictureUrl;
	}

	public String getArtisturl() {
		return url;
	}

	public void setArtisturl(String url) {
		this.url = url;
	}
	
	@Override
	public String toString() {
		return this.artistId + "\t" + this.artistName + "\t" + this.url + "\t" + this.pictureUrl;
	}

}
