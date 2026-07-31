function sendEmailSimulation(email, subject, body) {
  const delivered = Math.random() > 0.38;
  return { email, subject, body, delivered, channel: 'email' };
}

function sendNotificationSimulation(userId, message) {
  const delivered = Math.random() > 0.35;
  return { userId, message, delivered, channel: 'in_app' };
}

module.exports = {
  sendEmailSimulation,
  sendNotificationSimulation,
};
