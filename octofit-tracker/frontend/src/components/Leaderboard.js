import React, { useState, useEffect } from 'react';

function Leaderboard() {
  const [leaderboard, setLeaderboard] = useState([]);
  const [users, setUsers] = useState([]);
  const [teams, setTeams] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const leaderboardUrl = `https://${process.env.REACT_APP_CODESPACE_NAME}-8000.app.github.dev/api/leaderboard/`;
    const usersUrl = `https://${process.env.REACT_APP_CODESPACE_NAME}-8000.app.github.dev/api/users/`;
    const teamsUrl = `https://${process.env.REACT_APP_CODESPACE_NAME}-8000.app.github.dev/api/teams/`;
    console.log('Leaderboard API endpoint:', leaderboardUrl);

    Promise.all([
      fetch(leaderboardUrl).then(res => res.json()),
      fetch(usersUrl).then(res => res.json()),
      fetch(teamsUrl).then(res => res.json())
    ])
      .then(([leaderboardData, usersData, teamsData]) => {
        console.log('Leaderboard data fetched:', leaderboardData);
        console.log('Users data fetched:', usersData);
        console.log('Teams data fetched:', teamsData);
        
        const leaderboardArray = leaderboardData.results || leaderboardData;
        const usersArray = usersData.results || usersData;
        const teamsArray = teamsData.results || teamsData;
        
        setLeaderboard(Array.isArray(leaderboardArray) ? leaderboardArray : []);
        setUsers(Array.isArray(usersArray) ? usersArray : []);
        setTeams(Array.isArray(teamsArray) ? teamsArray : []);
        setLoading(false);
      })
      .catch(error => {
        console.error('Error fetching leaderboard:', error);
        setError(error.message);
        setLoading(false);
      });
  }, []);

  const getUserName = (userId) => {
    const user = users.find(u => (u._id || u.id) === userId);
    return user ? user.name : userId;
  };

  const getTeamName = (teamId) => {
    const team = teams.find(t => (t._id || t.id) === teamId);
    return team ? team.name : 'No Team';
  };

  if (loading) return (
    <div className="container mt-4">
      <div className="content-wrapper loading-container">
        <div className="spinner-border text-primary" role="status">
          <span className="visually-hidden">Loading...</span>
        </div>
        <p className="mt-3">Loading leaderboard...</p>
      </div>
    </div>
  );
  
  if (error) return (
    <div className="container mt-4">
      <div className="content-wrapper error-container">
        <p className="text-danger">Error: {error}</p>
      </div>
    </div>
  );

  return (
    <div className="container mt-4">
      <div className="content-wrapper">
        <h2 className="mb-4">🏆 Leaderboard</h2>
        <div className="table-responsive">
        <table className="table table-striped table-hover">
          <thead className="table-dark">
            <tr>
              <th>Rank</th>
              <th>User</th>
              <th>Team</th>
              <th>Total Duration (min)</th>
              <th>Total Calories</th>
            </tr>
          </thead>
          <tbody>
            {leaderboard.length > 0 ? (
              leaderboard.map((entry, index) => (
                <tr key={entry._id || entry.id || index}>
                  <td>{entry.rank || index + 1}</td>
                  <td>{getUserName(entry.user_id)}</td>
                  <td>{getTeamName(entry.team_id)}</td>
                  <td>{entry.total_duration || 0}</td>
                  <td>{entry.total_calories || 0}</td>
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan="5" className="text-center">No leaderboard data found</td>
              </tr>
            )}
          </tbody>
        </table>
        </div>
      </div>
    </div>
  );
}

export default Leaderboard;
