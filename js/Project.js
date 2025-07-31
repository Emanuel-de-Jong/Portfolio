class Project {
    constructor(name, repoName, imgPath,
            madeFor, pLangs,
            description) {
        imgPath = imgPath.replace(" ", "%20");

        this.name = name;
        this.repoName = repoName;
        this.imgPath = imgPath;

        this.madeFor = madeFor;
        this.pLangs = pLangs;

        this.description = description;
    }
}
