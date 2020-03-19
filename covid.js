const fs = require("fs"),
    spawn = require("child_process").spawn;

let covid = {};

covid.update_data = () =>
{
    const process = spawn('python', [
        "-u",
        "C:/Users/qasim/Desktop/Exigence/COVID-19/CoronaBluetooth/Diagnostics/get_updates.py"
        ]);
    process.stdout.on('data',async(data)=>{
        console.log(`data: ${data}`);   
    });
    process.stderr.on('error', async(data) => {
        console.log(`error: ${data}`);
    });
    process.stderr.on('close', async() => {
        console.log("Closed");
    });
}

covid.GitHub_Push = () =>
{
    const process = spawn('python', [
        "-u",
        "C:/Users/qasim/Desktop/Exigence/COVID-19/CoronaBluetooth/Diagnostics/github_push.py"
        ]);
    process.stdout.on('data',async(data)=>{
        console.log(`data: ${data}`);   
    });
    process.stderr.on('error', async(data) => {
        console.log(`error: ${data}`);
    });
    process.stderr.on('close', async() => {
        console.log("Closed");
    });
}

module.exports = covid;