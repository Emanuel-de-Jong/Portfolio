class Project {
    constructor(repoName, name, branch, madeFor,
            activeDateStart, activeDateEnd, lastChangeDate,
            description,
            imgPaths, pLangs) {
        this.repoName = repoName;
        this.name = name;
        this.branch = branch;
        this.madeFor = madeFor;

        this.activeDateStart = new Date(activeDateStart);
        this.activeDateEnd = new Date(activeDateEnd);
        this.lastChangeDate = new Date(lastChangeDate);

        this.description = description;

        this.imgPaths = imgPaths;
        this.pLangs = pLangs;
    }
}
