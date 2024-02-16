async function predict() {
    data = {}
    data["fixed.acidity"] = document.getElementById('op.fixed.acidity').innerHTML;
    data["volatile.acidity"] = document.getElementById('op.volatile.acidity').innerHTML;
    data["citric.acid"] = document.getElementById('op.citric.acid').innerHTML;
    data["residual.sugar"] = document.getElementById('op.residual.sugar').innerHTML;
    data["chlorides"] = document.getElementById('op.chlorides').innerHTML;
    data["free.sulfur.dioxide"] = document.getElementById('op.free.sulfur.dioxide').innerHTML;
    data["total.sulfur.dioxide"] = document.getElementById('op.total.sulfur.dioxide').innerHTML;
    data["density"] = document.getElementById('op.density').innerHTML;
    data["pH"] = document.getElementById('op.pH').innerHTML;
    data["sulphates"] = document.getElementById('op.sulphates').innerHTML;
    data["alcohol"] = document.getElementById('op.alcohol').innerHTML;

    const settings = {
        method: 'POST',
        body: JSON.stringify(data)
    };

    await fetch("http://localhost:5000/predict", settings).then(response => response.json()).then(
        function (response) {
            console.log("Response: ", response)
            document.getElementById("prediction").innerHTML = response.prediction;
        })
}

async function annotate() {

    data = {}
    data["fixed.acidity"] = document.getElementById('op.annotate.fixed.acidity').innerHTML;
    data["volatile.acidity"] = document.getElementById('op.annotate.volatile.acidity').innerHTML;
    data["citric.acid"] = document.getElementById('op.annotate.citric.acid').innerHTML;
    data["residual.sugar"] = document.getElementById('op.annotate.residual.sugar').innerHTML;
    data["chlorides"] = document.getElementById('op.annotate.chlorides').innerHTML;
    data["free.sulfur.dioxide"] = document.getElementById('op.annotate.free.sulfur.dioxide').innerHTML;
    data["total.sulfur.dioxide"] = document.getElementById('op.annotate.total.sulfur.dioxide').innerHTML;
    data["density"] = document.getElementById('op.annotate.density').innerHTML;
    data["pH"] = document.getElementById('op.annotate.pH').innerHTML;
    data["sulphates"] = document.getElementById('op.annotate.sulphates').innerHTML;
    data["alcohol"] = document.getElementById('op.annotate.alcohol').innerHTML;
    data["quality"] = document.getElementById('op.annotate.quality').innerHTML;

    const location = window.location.hostname;
    const settings = {
        method: 'POST',
        body: JSON.stringify(data)
    };
    console.log(data)

    await fetch("http://localhost:5000/annotate", settings).then(function (response) {
        console.log("Response: ", response.json)
        if (response.text == "Got it") {
            document.getElementById("annotate.status").innerHTML = "Added!!";
            setTimeout(function () {
                document.getElementById("annotate.status").innerHTML = "";
            }, 2000)
        }
    })
}