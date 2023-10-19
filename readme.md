<h1>Online Event Management System</h1>
<h2>Description:</h2>
<p>
Users can register, create, manage, and attend events. Additionally, they can RSVP, view event details, provide feedback. Event organizers can track attendance and manage event-related content.
</p>

<h3>The API Documentaion can be viewed here: <a href="https://documenter.getpostman.com/view/20090644/2s9YR9Zt8t">Docs</a></h3>

<h2>Operations:</h2>
<h3>User Registration:</h3>
<p>Users can register to the event management system.</p>

<p><a href="https://djoser.readthedocs.io/en/latest/introduction.html">Djoser</a> is used for the user registration.</p>
<h4>Register</h4>
<img src="images/register.png">

<h4>Activation Email</h4>
<img src="images/activation.png">
<img src="images/activation2.png">

<h4>Login</h4>
<img src="images/login.png">

<h3>Event Creation:</h3>
<p>Users can create and manage events.</p>

<h4>Create Event</h4>
<img src="images/createevent.png">
<p>Only auhtenticated users can create event so we pass the jwt token in the headers.</p>
<img src="images/jwt.png">

<h4>View all Event</h4>
<img src="images/viewevent.png">

<h4>Edit Event</h4>
<img src="images/editevent.png">
<p>Only the organizer can modify the event.</p>
<img src="images/permission.png">

<h3>RSVP:</h3>
<h4>Joing Event:</h4>
<img src="images/joinevent.png">

<h4>Event Details:</h4>
<img src="images/eventdetail.png">

<h3>Feedback:</h3>
<h4>Posting Feedback</h4>
<img src="images/feedbackpost.png">

<h4>Viewing Feedback</h4>
<img src="images/feedbackget.png">

<h3>Attendance</h3>
<h4>Viewing attendance</h4>
<img src="images/attendance.png">

<h3>Category</h3>
<h4>Filter using category</h4>
<img src="images/category.png">

<h3>Event Content</h3>
<h4>Add Content</h4>
<img src="images/addcontent.png">

<h4>View Content</h4>
<img src="images/viewcontent.png">

<h4>Edit Content</h4>
<img src="images/editcontent.png">

<h4>Delete Content</h4>
<img src="images/deletecontent.png">

<h3>Reminder day before the event:</h3>
<img src="images/reminder.png">

<h3>Event updates if there is any change in the eent.</h3>
<img src="images/updatereminder.png">