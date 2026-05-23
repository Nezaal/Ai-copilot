import os
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings

def visualize_embeddings():
    project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DB_DIR = os.path.join(project_dir, "data", "chroma_db")
    print("Loading embeddings...")
    embeddings = OllamaEmbeddings(model="gemma2:2b")
    vectorstore = Chroma(persist_directory=DB_DIR, embedding_function=embeddings)
    data = vectorstore.get(include=["embeddings", "documents"])

    emb_array = np.asarray(data["embeddings"])
    if emb_array.size == 0:
        print("Upload a PDF first!"); return

    if emb_array.ndim != 2 or emb_array.shape[0] < 3:
        print("Need at least 3 embedded PDF chunks for a 3D map."); return

    pca = PCA(n_components=3)
    emb_3d = pca.fit_transform(emb_array)

    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(emb_3d[:,0], emb_3d[:,1], emb_3d[:,2], c=np.arange(len(emb_3d)), cmap='viridis')
    plt.title("3D Map of your PDF Chunks")
    plt.show()

if __name__ == "__main__":
    visualize_embeddings()
