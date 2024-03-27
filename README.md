# Clipsphere: A YouTube Clone Built with Serverless Architecture

## Project Overview

Clipsphere is a YouTube clone application built with a distributed serverless architecture. This project aims to explore the benefits of serverless functions and compare its performance and latency against a traditional server-based architecture (to be implemented in a future phase).

## Technologies

Frontend: Next.js, Tailwind CSS
Backend API: FastAPI
Video Processing: Python, AWS Lambda
Database: PostgreSQL (AWS RDS or managed instance)
Storage: AWS S3

## Architecture

The application consists of three main components:

- UI: The user interface built with Next.js and Tailwind CSS for a modern and responsive user experience.
- REST API: The backend API developed with FastAPI, responsible for handling user requests and triggering video processing services.
- Video Processing Service: This service leverages AWS Lambda functions and queues for efficient video processing.

**Features**

1. Video playback without authentication
2. User authentication (signup, login, logout)
3. Single Sign-On (SSO) with Google OAuth2
4. Video upload (authenticated users only)
5. Like/dislike functionality for videos
6. Display of video views and likes count
7. Video quality selection

**Video Upload Process**

1. Authorization check: Only logged-in users can upload videos.
2. Video upload to S3: The uploaded video is stored in an S3 bucket for raw video files.
3. Metadata storage: Video metadata is saved in a relational database (RDS or managed PostgreSQL).
4. Lambda triggered by upload: Uploading a video triggers a Lambda function for video transcoding.
5. Transcoded video storage: Transcoded versions are uploaded to a separate S3 bucket for efficient playback.

**Getting Started**

This repository is currently under development. We will soon provide instructions on setting up and running the application locally.
