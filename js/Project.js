class Project {
    constructor(name, repoName, imgPaths,
            madeFor, pLangs,
            description) {
        let correctedImgPaths = [];
        for (let i = 0; i < imgPaths.length; i++) {
            correctedImgPaths[i] = imgPaths[i].replace(" ", "%20");
        }

        this.name = name;
        this.repoName = repoName;
        this.imgPaths = correctedImgPaths;

        this.madeFor = madeFor;
        this.pLangs = pLangs;

        this.description = description;
    }
}
