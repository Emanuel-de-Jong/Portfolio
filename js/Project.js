class Project {
    constructor(name, branch, date, imgPaths,
            madeFor, pLangs,
            description) {
        let correctedImgPaths = [];
        for (let i = 0; i < imgPaths.length; i++) {
            correctedImgPaths[i] = imgPaths[i].replace(" ", "%20");
        }

        this.name = name;
        this.branch = branch;
        this.date = new Date(date);
        this.imgPaths = correctedImgPaths;

        this.madeFor = madeFor;
        this.pLangs = pLangs;

        this.description = description;
    }
}
