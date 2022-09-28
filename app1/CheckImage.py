image = images[10] # take an existing image or create a numpy array from PIL image
image = np.expand_dims(image, 0) # add a batch dimension
feature = vectorizer.predict(image)

distances, nbors = knn.kneighbors(feature)
# output is a tuple of list of distances and list nbors of each image
# so we take the first entry from those lists since we have only one image
distances, nbors = distances[0], nbors[0]

nbor_images = [images[i] for i in nbors]
fig, axes = plt.subplots(1, len(nbors)+1, figsize=(10, 5))

for i in range(len(nbor_images)+1):
    ax = axes[i]
    ax.set_axis_off()
    if i == 0:
        ax.imshow(image.squeeze(0))
        ax.set_title("Input")
    else:
        ax.imshow(nbor_images[i-1])
        # we get cosine distance, to convert to similarity we do 1 - cosine_distance
        ax.set_title(f"Sim: {1 - distances[i-1]:.2f}")