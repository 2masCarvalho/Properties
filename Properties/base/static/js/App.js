import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import MyProperties from './MyProperties';

function App() {
  return (
    <Router>
      <Switch>
        <Route path="/myproperties/:userId">
          <MyProperties />
        </Route>
        {/* Other routes */}
      </Switch>
    </Router>
  );
}

export default App;