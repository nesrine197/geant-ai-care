function Message({ message }) {
  return (
    <div className={`message ${message.role}`}>
      <div className="message-content">
        {message.text}
      </div>
    </div>
  );
}

export default Message;