This repository contains all work related to ICS5114:

* deliverable - VLE Submission
	* SourceCode/
	* Demo_SpeechAnalyticsOnLiveStreams.pptx
	* PlagiarismForm.pdf
	* Presentation_SpeechAnalyticsOnLiveStreams.pptx
	* README.txt
	* Report Documentation.pdf
* docker - Docker Scripts
	* 000_Base/
	* 001_Producer/
	* 002_Kafka/
	* 003_Storm/
	* 004_Neo4j/
	* 005_VMAutomation
	* buildDockerImages.sh
	* uploadDockerImages.sh
* docs - Error Logs, Documentation, Final Report and Presentations
	* Demo_SpeechAnalyticsOnLiveStreams.pptx
	* PlagiarismForm.pdf
	* Presentation_SpeechAnalyticsOnLiveStreams.pptx
	* Report Documentation.pdf
* milestones - Contains data captured and visualizations pertaining to both milestone runs
	* milestone1/
	* milestone2/
	* Architecture_Wireframes.pdf
	* GeekandSundry Entire Pipeline Simulation.png
	* graph.png
	* John Oliver Snippet.png
* prototype - Contains 1-off scripts with varied pipeline prototypes
	* text_scraping/
	* blob_downloader.py
	* streamlink call
	* universal_video_capture.py
	* youtube_livestream_capture.py
* recording - Contains logic pertaining to the producer class, responsible for feeding data down the pipeline
	* src/
* streaming - Contains Storm logic for Spouts and Bolts, including Kafka-Consumer, and Neo4j graph writing
	* src/
	* topologies/
	* venv/
	* virtualenvs/
	* config.json
	* fabfile.py
	* installationScript.sh
	* project.clj
	* README.md
* visualizations - Contains scripts dedicated to connecting to a Neo4j graph instance, and rendering a number of visualizations
	* utils/
	* visuals/
	* main.py
