- The dist folder is the build React app
- The app.py file is where to put the result of the data
- Feel free to create new python file
- After installing the dependencies or packages run the app.py file and open http://127.0.0.1:3000 to see the interface
- If installing the packages doesn't work. Try to manually install. I only install two packages.
  pip install flask and pip install flask-cors
- The python version needs to be between 3.9 and 3.12
- The legal_prediction.py is the model file. Using the qa_system_with_crime as a function to transform user's input into answers
- There are two missing files, which is the with_hie_with_kg_embeddings.pkl and output_bgecriminal_all_predictions_with_law.json. The reason it's not uploaded into GitHub is because the size is to enormous.

```bash
pip install flask
pip install flask-cors
pip install FlagEmbedding
```

Basically these three packages are important. There might be some error when installing or using this repository on different environment.

```
/Criminal_System
|
|-- /dist
| |-- /assets
| |-- index.html
|-- app.py # The main python file (web app)
|-- legal_prediction.py # The model python file (BGE-M3)
```
