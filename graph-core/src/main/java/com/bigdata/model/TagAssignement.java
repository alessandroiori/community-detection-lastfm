package com.bigdata.model;

import java.io.Serializable;

public class TagAssignement implements Serializable {
	
	/**
	 * 
	 */
	private static final long serialVersionUID = 1L;

	private Long artistId;

	private Long userId;
	
	private Long tagId;

	private Integer timestamp;

	public Long getArtistid() {
		return artistId;
	}

	public void setArtistid(Long artistId) {
		this.artistId = artistId;
	}

	public Long getUserid() {
		return userId;
	}

	public void setUserid(Long userId) {
		this.userId = userId;
	}

	public Long getTagid() {
		return tagId;
	}

	public void setTagid(Long tagId) {
		this.tagId = tagId;
	}

	public Integer getTimestamp() {
		return timestamp;
	}

	public void setTimestamp(Integer timestamp) {
		this.timestamp = timestamp;
	}
	
	@Override
	public String toString() {
		return this.userId + "\t" + this.artistId + "\t" + this.tagId + "\t" + this.timestamp;
	}

}
