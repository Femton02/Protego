function generateReport(matches) {
    const reportedLocations = new Set();
    let vulnerabilityCount = 0;

    if (matches.length === 0) {
        console.log("No vulnerabilities found.");
    } else {
        console.log("Vulnerabilities found:");
        matches.forEach(match => {
            const locationKey = `Start ${match.location.start}, End ${match.location.end}`;
            if (!reportedLocations.has(locationKey)) {
                vulnerabilityCount++;
                console.log(`#${vulnerabilityCount}:`);
                console.log(`Rule: ${match.rule}`);
                console.log(`Description: ${match.description}`);
                console.log(`Location: ${locationKey}`);
                console.log("------------");

                reportedLocations.add(locationKey);
            }
        });
    }
}

module.exports = {
    generateReport
};
