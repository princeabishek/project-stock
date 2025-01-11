const functions = require('@google-cloud/functions-framework');
const dialogflow = require('@google-cloud/dialogflow');
const cors = require('cors')({ origin: true });

const CREDENTIALS = {
    client_email: "market-mentor@newagent-cnle.iam.gserviceaccount.com",
    private_key: "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCGyTzQH1WUHI+3\ncfVEaBYeMiihWX/dHx2YRQa2wf8J0S9pqSS1lIPfAwTecBLAbh5HRUreVJlg7mXd\nEKLQlmM0vmdcRnrymszuH/wi4x2K7P/MqbwVchVjTyAzjEHTMRi/kmYV+1SwMN7Z\n0Hq10+NT50sRFzgtqlRJ3xseT5utxDJwMW0EpoaBEF9mIscUGT1KvmQy74AN+JoQ\n55jG/LcpKBjahmcxCnDMtPXqfS2gvo/WYKSL9QqfzKM5c8sBEMRJ2lh/vsOM/O51\nkm1DlGdIUxJC6RzuSFjol4LjIamB33pquqO+OGIReQP81GEorSdGp/6JSbMpoD1N\nYuuhZQypAgMBAAECggEABFZjg5sOiPamVVPwfaQP2ibpEdAsgjQnIqhOAAGcMHev\n2+maidFesQWK2ZGnuNOSW97J+v+j8++YDZYkdyvvw1nBP8Hw4O/EWoFi/shqQfdA\ngBiSOepy78AzHBWOZLp2vmt6p4hwAD+CXGYOHN3VufR+gO1LXITXs4zfdYlATEYx\nGF0esPxF1zbHG0k1o+Tp/NQ1gqrnRLSjYPo3WDyKB4CqaBNJHYDWPiqCJH1fb7XI\n0k/BwgYIjA556FdSWFiKnjH8kFmsmWVhrSouzOnnBw7ciweytPgMtJNVAcd6pTL0\n46HwWbsIqH5euU8+pwXGMewSo44B6dglqLMSeCwo9QKBgQC8lzXlqkoAmUXLVZSX\n1INdxQAaxyDbxJr9RsJNwqNRfsKXOJWrm2CNtLudFfL7uxQh5h9na8VjoV1e205H\nXxM/8If6Pi/J+Gr1zlkNZ/t+mAQWKSc4wo3Hso3X3MBnWkUcWktcBn+4L3hmHQsR\nXGhGzO8+rAjMaKoOnPVTKLJ7uwKBgQC29rIVmlXeNtvlv6zITTwQG4IJ87UopKh/\nGNod7aoV6TB47KEU0/CQTxzgDYcrVRHn6xYjik0zbMU2MB0tP1GE/N/uippkJb+a\nZHrOEDFgA7aS/qjL7y/8UVhBKgIKmYKQuz5dPis0E2cJ8f90LkvE9UI1xhysBYlc\nWS9tG4To6wKBgEAM0v9HUI7Xf37JeAgA4wTLzXdKvfwlz8XJbGBghHs/I/OcAikg\nQjCee0GknLumE/ZXY78KOSXXPhDjRriyr6T9mhEBYdWkix8kj9YfxKiAFJM6Mtny\nKZjzKX1wud/gJqy0dfexNVtms+tqXcHtsnSpUW/lma9itK7129P8dHHVAoGBAKbT\nyEu0XylwYg9aN4SoD+Ur/+VtJzj48n55PaDebSDvcHhCYxonqgkbadvN2fsj5WDP\nVW9wkrYaLrQbKO9x9bXKEbFjBiXc2ZlAl00/LJY8rIPZ2jWhUeLClTNNx3C8ynWH\nlfTVU/V235QM6X2ZHRNpAkcf7lLX9YiT9Y+J8SWjAoGAAo0hjxOdry0zaZkd+ovJ\nwqAEmmioXBA5QVBLjy8JhXImZQlBvZUEHVs+dBkWAXKFydtlHxrHLvWP69BVjjPG\nKLpdzHyl3Ya4bPpi4FST6v9fejMBNk/e/MmR+R1oidMCq17jRim/jax5d7viZyf3\nlOJ+I/gYCv9gS0K/HWfp3ak=\n-----END PRIVATE KEY-----\n",
    project_id: "newagent-cnle"
};

functions.http('dialogflow', async (req, res) => {
    cors(req, res, async () => {
        try {
            const { sessionId, queryInput } = req.body;
            const sessionClient = new dialogflow.SessionsClient({
                credentials: CREDENTIALS,
                projectId: CREDENTIALS.project_id
            });

            const sessionPath = sessionClient.projectAgentSessionPath(
                CREDENTIALS.project_id,
                sessionId
            );

            const request = {
                session: sessionPath,
                queryInput: queryInput
            };

            const responses = await sessionClient.detectIntent(request);
            const result = responses[0].queryResult;

            res.json({
                fulfillmentMessages: result.fulfillmentMessages,
                intent: result.intent.displayName,
                confidence: result.intentDetectionConfidence
            });
        } catch (error) {
            console.error('Error:', error);
            res.status(500).send({ error: 'Error processing Dialogflow request' });
        }
    });
});
