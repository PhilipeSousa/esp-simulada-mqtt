const mqtt = require("mqtt");
const express = require("express");
const parser = require("body-parser");

// pega as var de ambiente
require("dotenv").config();

// Cria aplicação com o middleware para garantir 
// que os dados sejam analisado com json  
const app = express();
app.use(parser.json());

const brokerUrl = "mqtt://test.mosquitto.org";
const topicoData = process.env.TOPIC_DATA;
const topicoCommand = process.env.TOPIC_COMMAND;


//console.log(topicoData, topicoCommand, brokerUrl)

const client = mqtt.connect(brokerUrl);

// callback ao se conectar ao broker e receber mensagens
client.on("connect", () =>{
    console.log("Conectado ao Broker");
    // Agr tenta se inscrever no topico 
    client.subscribe(topicoData, (err) =>{
        if (err) console.log("Erro ao se inscrever no topico: ", err);
        else console.log(`Inscrito no topico ${topicoData}`);
    });
})

client.on("message", (topico, msg)=>{
    if (topicoData == topico){
        const dadosDoSensor = JSON.parse(msg.toString());
        console.log("Dados recebidos:", dadosDoSensor);
    }
})


// endpoint para enviar comandos para placas

app.post("/send-command", (req, res)=>{
    const {dispositivo, estado } = req.body;

    if(!dispositivo || !estado ) return res.status(400).send(" 'dispositivo' e 'estado' são obrigatórios");

    const command = {
        Tipo: "comando",
        Dispositivo: dispositivo,
        Estado: estado,
    };

    client.publish(topicoCommand, JSON.stringify(command));
    console.log("Comando enviado: ", command);
    res.send("Enviado com sucesso");
});


const PORT = 3000;
app.listen(PORT, ()=>{
    console.log(`Serviço rodando em http://localhost:${PORT}`);
});
