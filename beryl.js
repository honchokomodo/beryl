const Discord = require("discord.js");

const keys = require("./penis_pleasure_18.json");

const intents = new Discord.Intents(32767);

const client = new Discord.Client({intents});

client.on("ready", () => {
	console.log("ready");
	client.api.applications(client.user.id).commands.post({data: [
		{
			name: "testcommand",
			description: "this is a test. this is a test of the outdoor warning system. this is only a test."
		},
		{
			name: "cat",
			description: "returns"
		}
	]});
});

/*
client.on('interactionCreate', async interaction => {
	if (!interaction.isCommand()) return;
	if (interaction.commandName === "testcommand") await interaction.reply('Pong!');
});
*/

client.ws.on("INTERACTION_CREATE", async interaction => {
	client.api.interactions(interaction.id, interaction.token).callback.post({data: {
		type: 4,
		data: {
			content: "Hello World!"
		}
	}})
});

client.login(keys.botkey_nodejs);

