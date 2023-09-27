<?php
    // Create a database connection
    $mysqli = new mysqli("", "", "", "");

    // Check connection
    if ($mysqli->connect_error) {
        die("Connection failed: " . $mysqli->connect_error);
    }

    // Query to get the resource value (assuming you have a 'resources' table)
    $resourceResult = $mysqli->query("SELECT resources_amount, date FROM resources ORDER BY id DESC LIMIT 1");

    if ($resourceResult->num_rows > 0) {
        $resourceRow = $resourceResult->fetch_assoc();
        $resourceValue = $resourceRow["resources_amount"];
        $resourceDate = $resourceRow["date"];
    } else {
        // If no data is available, set a default value
        $resourceValue = 0;
        $resourceDate = "Unknown";
    }

    $researchResult = $mysqli->query("SELECT research_level, date FROM research ORDER BY id DESC LIMIT 1");

    if ($researchResult->num_rows > 0) {
        $researchRow = $researchResult->fetch_assoc();
        $researchValue = $researchRow["research_level"];
        $researchDate = $researchRow["date"];
    } else {
        // If no data is available, set a default value
        $researchValue = 0;
        $researchDate = "Unknown";
    }
    $imageResult = $mysqli->query("SELECT image FROM research_screenshots ORDER BY id DESC LIMIT 1");

    if ($imageResult->num_rows > 0) {
        $imageRow = $imageResult->fetch_assoc();
        $researchImage = $imageRow["image"];
    }



    // Close the database connection
    $mysqli->close();



    ?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-T3c6CoIi6uLrA9TneNEoa7RxnatzjcDSCmG1MXxSR1GAsXEV/Dwwykc2MPK8M2HN" crossorigin="anonymous">
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-C6RzsynM9kWDrMNeT87bh95OGNyZPhcTNXj1NW7RuBCsyN/o0jlpcV8Qyq46cDfL" crossorigin="anonymous"></script>
    <title>Resource Monitor</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            text-align: center;
        }
        header {
            background-color: #333;
            color: #fff;
            padding: 20px 0;
        }
        main {
            padding: 20px;
        }
        .resource-progress-container, .research-progress-container {
            margin: auto;
            width: 80%;
        }
        p {
            font-weight: bold;
        }
        a{
        font-weight: bold;
        font-size: 20px;
        }
        .progress{
        height: 50px;
        }
    </style>
</head>
<body>
    <header>
        <h1>Resource Monitor</h1>
    </header>
    <main>
        <div class="resource-progress-container">
            <div class="progress" role="progressbar" aria-label="Animated striped example" aria-valuenow="25" aria-valuemin="0" aria-valuemax="100">
                <div class="progress-bar progress-bar-striped progress-bar-animated bg-danger" style="width: 100%" id="resource-progress-bar"><a id="resource-value">Loading...</a></div>
            </div>
        </div>
        <p id="resource-date">Loading...</p>
        <br><br>

        <div class="research-progress-container">
            <div class="progress" role="progressbar" aria-label="Animated striped example" aria-valuenow="25" aria-valuemin="0" aria-valuemax="100">
                <div class="progress-bar progress-bar-striped progress-bar-animated bg-danger" style="width: 100%" id="research-progress-bar"><a id="research-value">Loading...</a></div>
            </div>
        </div>
        <p id="research-date">Loading...</p>
        <?php
        if (!empty($researchImage)) {
            echo "<img src='data:image/png;base64,". base64_encode($researchImage) ."' alt='' width='360' height='360'>";
        } else {
            echo "<div class='alert alert-warning' style='width: 22%; margin: auto;' role='alert'>";
            echo "Image of current project was not found in database";
            echo "</div>";
        }
?>
    </main>
    <script>
        function updateResourcesProgressBar() {
        //* Resources progress bar
        const resourceValue = <?php echo $resourceValue ?>;
        const resourceDateText = "<?php echo $resourceDate ?>"; // Renamed variable

        const resourceProgressBar = document.getElementById("resource-progress-bar");
        const resourceText = document.getElementById("resource-value");
        const resourceDateElement = document.getElementById("resource-date");

        if (resourceValue == 0 || resourceValue == null) {
            resourceText.textContent = "Resource level was not found!";
            resourceProgressBar.style.width = "100%";
            resourceDateElement.textContent = "" ;
            resourceProgressBar.classList.add("bg-danger");
        } else {
            if (resourceValue >= 60) {
                resourceProgressBar.classList.remove("bg-danger");
                resourceProgressBar.classList.add("bg-success");
            } else if (resourceValue < 60 && resourceValue >= 40) {
                resourceProgressBar.classList.remove("bg-danger");
                resourceProgressBar.classList.add("bg-warning");
            } else {
                resourceProgressBar.classList.remove("bg-success");
                resourceProgressBar.classList.add("bg-danger");
            }
            resourceText.textContent = "Resource Level: " + resourceValue + "%";
            resourceDateElement.textContent = "Resource Level from: " + resourceDateText; // Updated variable name
            resourceProgressBar.style.width = resourceValue + "%";
        }
    }
    function updateResearchProgressBar() {
        //* Research progress bar

        const researchValue = <?php echo $researchValue ?>;
        const researchDateText = "<?php echo $researchDate ?>"; // Renamed variable

        // Update the progress bar width and text based on the research value
        const researchProgressBar = document.getElementById("research-progress-bar");
        const researchText = document.getElementById("research-value");
        const researchDateElement = document.getElementById("research-date");

        if (researchValue == "NULL" || researchValue === 0) {
            researchText.textContent = "Research level was not found!";
            researchProgressBar.style.width = "100%";
            researchDateElement.textContent = "" ;
            researchProgressBar.classList.add("bg-danger");
        } else {
            researchProgressBar.classList.remove("bg-danger");
            researchProgressBar.classList.add("bg-info");
            researchText.textContent = "Research progress: " + researchValue + "%";
            researchDateElement.textContent = "Research progress from: " + researchDateText;
            researchProgressBar.style.width = researchValue + "%";
        }
    }
    document.addEventListener("DOMContentLoaded", () => {
            updateResearchProgressBar()
            updateResourcesProgressBar()
    });
</script>
</body>
</html>
