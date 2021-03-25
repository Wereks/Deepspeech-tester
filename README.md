Script to partially automate testing the DeepSpeech model from Mozilla. 
It can transcript .wav audio files and analyze results with defined metrics.
Which can be further analyzed and saved into a .csv file.


The structure of the workspace folder should be:
```
├───workspace
│   └───test1
│       │   expected.txt
│       │   result.json
│       │   tags.toml
│       │
│       └───audio
│               my_audio_file copy 2.wav
│               my_audio_file copy.wav
│               my_audio_file.wav
```
Only the files in audio can have a different name (must be .wav), also 'test1' can be renamed. 

##### tags.toml
```
code = "000000" #required

[Tags] #notrequired
````

##### expected.txt
```
[my_audio_file copy 2]
experience
proves 
this
[my_audio_file copy]
experience proves this
[my_audio_file]
experience proves this
```

