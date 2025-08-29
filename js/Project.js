class Project {
    constructor(repoName, name, branch, madeFor,
            activeDateStart, activeDateEnd, lastChangeDate,
            description,
            imgPaths, skills) {
        this.repoName = repoName;
        this.name = name;
        this.branch = branch;
        this.madeFor = madeFor;

        this.activeDateStart = new Date(activeDateStart);
        this.activeDateEnd = new Date(activeDateEnd);
        this.lastChangeDate = new Date(lastChangeDate);

        this.workDays = this.calcWorkDays();

        this.description = description;

        this.imgPaths = imgPaths;
        this.skills = skills;
    }

    calcWorkDays() {
        const start = this.activeDateStart;
        const end = this.activeDateEnd;
        // Normalize dates to midnight UTC to prevent DST issues.
        const startUTC = Date.UTC(start.getFullYear(), start.getMonth(), start.getDate());
        const endUTC = Date.UTC(end.getFullYear(), end.getMonth(), end.getDate());

        const msDifference = endUTC - startUTC;
        const msInDay = 1000 * 60 * 60 * 24;
        // Add 1 to include both start and end day.
        return Math.floor(msDifference / msInDay) + 1;
    }
}
