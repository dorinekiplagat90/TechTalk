// Notifications page - shows user notifications
import { useState, useEffect, useContext } from 'react';
import { AuthContext } from '../context/AuthContext';
import { formatDate } from '../utils/date';
import api from '../utils/api';
import LoginRequired from './LoginRequired';

const Notifications = () => {
  const { user } = useContext(AuthContext);
  const [notifications, setNotifications] = useState([]);

  if (!user) {
    return <LoginRequired />;
  }

  useEffect(() => {
    loadNotifications();
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const loadNotifications = async () => {
    try {
      const response = await api.get('/notifications');
      setNotifications(response.data);
    } catch (error) {
      console.error('Error loading notifications:', error);
    }
  };

  const markAsRead = async (id) => {
    try {
      await api.put(`/notifications/${id}/read`);
      loadNotifications();
    } catch (error) {
      console.error('Error marking notification as read:', error);
    }
  };

  const markAllAsRead = async () => {
    try {
      await api.put('/notifications/read-all');
      loadNotifications();
    } catch (error) {
      console.error('Error marking all as read:', error);
    }
  };

  return (
    <div className="app-bg">
      <div className="container mx-auto px-4 py-6 max-w-2xl">
        <div className="flex justify-between items-center mb-6">
          <h1 className="text-2xl font-bold">Notifications</h1>
          {notifications.some((n) => !n.read) && (
            <button
              onClick={markAllAsRead}
              className="text-[#1f6feb] hover:underline"
            >
              Mark all as read
            </button>
          )}
        </div>

        {notifications.length === 0 ? (
          <div className="card-dark p-8 text-center">
            No notifications yet.
          </div>
        ) : (
          <div className="card-dark">
            {notifications.map((notification) => (
              <div
                key={notification.id}
                className={`p-4 border-b border-[#1f3b5c] ${notification.read ? '' : 'bg-[#1f6feb]/10'}`}
              >
                <div className="flex justify-between items-start">
                  <div className="flex-1">
                    <p className="font-medium">{notification.message}</p>
                    <p className="text-sm text-[#8b949e] mt-1">
                      {formatDate(notification.timestamp)}
                    </p>
                  </div>
                  {!notification.read && (
                    <button
                      onClick={() => markAsRead(notification.id)}
                      className="text-[#1f6feb] text-sm hover:underline"
                    >
                      Mark as read
                    </button>
                  )}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default Notifications;