# Movie Star Baby Names

## Introduction

As part of my exploration of the ["baby names" dataset](https://catalog.data.gov/dataset/baby-names-from-social-security-card-applications-national-level-data), I started to wonder how pop culture had an effect on the popularity of names.  There are various components of pop culture, but I decided to look into the effect popular movies and their stars had on popularity of names.

How should I look at this?  I'd want to see the overall popularity of the name, of course, but it might also be interesting to see if there is a spike when a movie star comes out with a new movie.  Did "Godfather" result in a lot of kids named Marlon or Al?  Did more kids get the name Quentin, John, Uma, or Samuel after "Pulp Fiction"?  

This project is a web app to satisfy your curiosities about these questions.

## Repo

This repo is a work in progress.  

I've built functionality to do the following:

* Combine the ["baby names" dataset](https://catalog.data.gov/dataset/baby-names-from-social-security-card-applications-national-level-data)
* Load and segment the baby names dataset
* An API to segment the baby names dataset
* Scrape IMDB to get an actor's page
* Scrape IMDB to get an actor's "Known For" movies
* An API to return an actor's "Known For" movies
* **TODO** A webapp to plot an actor's first name over time along with their most popular movies