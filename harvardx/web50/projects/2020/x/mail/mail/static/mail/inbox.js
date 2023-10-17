document.addEventListener('DOMContentLoaded', function () {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');

  document.querySelector('#compose-form').onsubmit = function () {
    event.preventDefault()
    fetch('/emails', {
      method: 'POST',
      body: JSON.stringify({
        recipients: document.querySelector('#compose-recipients').value,
        subject: document.querySelector('#compose-subject').value,
        body: document.querySelector('#compose-body').value
      })
    })
      .then(response => response.json())
      .then(result => {
        // Print result
        console.log(result);
      });
  }

  function compose_email() {

    // Show compose view and hide other views
    document.querySelector('#emails-view').style.display = 'none';
    document.querySelector('#compose-view').style.display = 'block';
    document.querySelector('#email-view').style.display = 'none';

    // Clear out composition fields
    document.querySelector('#compose-recipients').value = '';
    document.querySelector('#compose-subject').value = '';
    document.querySelector('#compose-body').value = '';
  }

  function load_email(id) {
    event.preventDefault()
    fetch('/emails/' + id)
      .then(response => response.json())
      .then(email => {

        // Print email

        document.querySelector('#emails-view').style.display = 'none';
        document.querySelector('#compose-view').style.display = 'none';
        document.querySelector('#email-view').style.display = 'block';

        document.querySelector('#email-view').innerHTML = `
        <div class="card" style="width: 100%; height: 80%;">
          <div class="card-body">
            <h5 class="card-title">${email['sender']}</h5>
            <h6 class="card-subtitle mb-2 text-muted">${email['timestamp']}</h6>
            <p class="card-text">Subject: ${email['subject']}</p>

            <p class="card-text">${email['body']}</p>

          </div>
        </div>
        `;
        fetch('/emails/' + id, {
          method: 'PUT',
          body: JSON.stringify({
            read: true
          })
        })
        const reply = document.createElement('a');
        reply.className = "btn btn-primary";
        reply.innerHTML = "Reply";
        reply.style.color = 'white'
        reply.style.margin = '10px'
        reply.addEventListener('click', function() {compose_email(); document.querySelector('#compose-recipients').value = email['sender']; document.querySelector('#compose-subject').disabled = true; document.querySelector('#compose-subject').value = "re: " + email['subject']; document.querySelector('#compose-body').value = `On ${email['timestamp']} ${email['sender']} wrote: ${email['body']}`})
        document.querySelector('#email-view').append(reply);

        if (email.archived === false) {
          const archive = document.createElement('a');
          archive.className = "btn btn-primary";
          archive.innerHTML = "Archive";
          archive.style.color = 'white'
          archive.style.margin = '10px'

          archive.addEventListener('click', () =>
            fetch('/emails/' + id, {
              method: 'PUT',
              body: JSON.stringify({
                archived: true
              })
            })
              .then(response => load_mailbox('archive'))
          );
          document.querySelector('#email-view').append(archive);
        } else {
          const archive = document.createElement('a');
          archive.className = "btn btn-primary";
          archive.innerHTML = "Archived";
          archive.style.color = 'white'
          archive.style.margin = '10px'
          archive.style.background = '#2E2D37'
          archive.style.border = '#2E2D37'

          archive.addEventListener('click', () =>
            fetch('/emails/' + id, {
              method: 'PUT',
              body: JSON.stringify({
                archived: false
              })
            })
              .then(response => load_mailbox('inbox'))
          );
          document.querySelector('#email-view').append(archive);
        }





      })
  }

  function load_mailbox(mailbox) {

    // Show the mailbox and hide other views
    document.querySelector('#emails-view').style.display = 'block';
    document.querySelector('#compose-view').style.display = 'none';
    document.querySelector('#email-view').style.display = 'none'

    // Show the mailbox name
    document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

    fetch('/emails/' + mailbox)
      .then(response => response.json())
      .then(emails => {
        // Print emails
        emails.forEach(email => {
          const email_card = document.createElement('div');
          email_card.className = "card w-75"
          if (email.read === false) {
            email_card.style.background = 'white'
          } else {
            email_card.style.background = '#e3e1e1'
          }
          email_card.innerHTML = `
          <div class="post-header">
            <strong>${post['sender']} |</strong>
            <h10 class="text-muted"></h10>
          </div>
            `;



          email_card.addEventListener('click', () => load_email(email['id']));
          document.querySelector('#emails-view').append(email_card);

        })

        console.log(emails);

        // ... do something else with emails ...
      });

  }

});

