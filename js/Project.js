class Project {
    constructor(name, branch, date, madeFor, description, imgPaths, pLangs) {
        this.name = name;
        this.branch = branch;
        this.date = new Date(date);
        this.imgPaths = imgPaths;

        this.madeFor = madeFor;
        this.pLangs = pLangs;

        this.description = description;
    }
}
