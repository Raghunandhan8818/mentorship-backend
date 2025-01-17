from datetime import datetime, timedelta

from app.database.models.mentorship_relation import MentorshipRelationModel
from app.database.models.tasks_list import TasksListModel
from app.database.models.user import UserModel
from app.database.sqlalchemy_extension import db
from app.utils.enum_utils import MentorshipRelationState
from tests.base_test_case import BaseTestCase
from tests.test_data import user1, user2, user4, user5


class TasksBaseTestCase(BaseTestCase):
    # Setup consists of adding 2 users into the database
    # User 1 is the mentorship relation requester = action user
    # User 2 is the receiver
    def setUp(self):
        super().setUp()

        self.first_user = UserModel(
            name=user1["name"],
            email=user1["email"],
            username=user1["username"],
            password=user1["password"],
            terms_and_conditions_checked=user1["terms_and_conditions_checked"],
        )
        self.second_user = UserModel(
            name=user2["name"],
            email=user2["email"],
            username=user2["username"],
            password=user2["password"],
            terms_and_conditions_checked=user2["terms_and_conditions_checked"],
        )

        self.fourth_user = UserModel(
            name=user4["name"],
            email=user4["email"],
            username=user4["username"],
            password=user4["password"],
            terms_and_conditions_checked=user4["terms_and_conditions_checked"],
        )

        self.fifth_user = UserModel(
            name=user5["name"],
            email=user5["email"],
            username=user5["username"],
            password=user5["password"],
            terms_and_conditions_checked=user5["terms_and_conditions_checked"],
        )

        # making sure both are available to be mentor or mentee
        self.first_user.need_mentoring = True
        self.first_user.available_to_mentor = True
        self.first_user.is_email_verified = True
        self.second_user.need_mentoring = True
        self.second_user.available_to_mentor = True
        self.second_user.is_email_verified = True
        self.fourth_user.available_to_mentor = True
        self.fourth_user.is_email_verified = True
        self.fifth_user.need_mentoring = True
        self.fifth_user.is_email_verified = True

        self.notes_example = "description of a good mentorship relation"

        self.now_datetime = datetime.utcnow()
        self.end_date_example = self.now_datetime + timedelta(weeks=5)

        self.tasks_list_1 = TasksListModel()
        self.tasks_list_2 = TasksListModel()
        self.tasks_list_3 = TasksListModel()
        self.tasks_list_4 = TasksListModel()

        db.session.add(self.tasks_list_1)
        db.session.add(self.tasks_list_2)
        db.session.add(self.tasks_list_3)
        db.session.add(self.tasks_list_4)
        db.session.add(self.first_user)
        db.session.add(self.second_user)
        db.session.add(self.fourth_user)
        db.session.add(self.fifth_user)
        db.session.commit()

        # create new mentorship relation

        self.mentorship_relation_w_second_user = MentorshipRelationModel(
            action_user_id=self.first_user.id,
            mentor_user=self.first_user,
            mentee_user=self.second_user,
            creation_date=self.now_datetime.timestamp(),
            end_date=self.end_date_example.timestamp(),
            state=MentorshipRelationState.ACCEPTED,
            notes=self.notes_example,
            tasks_list=self.tasks_list_1,
        )

        self.mentorship_relation_w_admin_user = MentorshipRelationModel(
            action_user_id=self.first_user.id,
            mentor_user=self.first_user,
            mentee_user=self.admin_user,
            creation_date=self.now_datetime.timestamp(),
            end_date=self.end_date_example.timestamp(),
            state=MentorshipRelationState.ACCEPTED,
            notes=self.notes_example,
            tasks_list=self.tasks_list_2,
        )

        self.mentorship_relation_without_first_user = MentorshipRelationModel(
            action_user_id=self.second_user.id,
            mentor_user=self.second_user,
            mentee_user=self.admin_user,
            creation_date=self.now_datetime.timestamp(),
            end_date=self.end_date_example.timestamp(),
            state=MentorshipRelationState.COMPLETED,
            notes=self.notes_example,
            tasks_list=self.tasks_list_3,
        )

        self.mentorship_relation_bw_fourth_fifth_user = MentorshipRelationModel(
            action_user_id=self.fourth_user.id,
            mentor_user=self.fourth_user,
            mentee_user=self.fifth_user,
            creation_date=self.now_datetime.timestamp(),
            end_date=self.end_date_example.timestamp(),
            state=MentorshipRelationState.COMPLETED,
            notes=self.notes_example,
            tasks_list=self.tasks_list_4,
        )

        db.session.add(self.mentorship_relation_w_second_user)
        db.session.add(self.mentorship_relation_w_admin_user)
        db.session.add(self.mentorship_relation_without_first_user)
        db.session.add(self.mentorship_relation_bw_fourth_fifth_user)
        db.session.commit()

        self.description_example = "This is an example of a description"

        self.tasks_list_1.add_task(
            description=self.description_example,
            created_at=self.now_datetime.timestamp(),
        )
        self.tasks_list_1.add_task(
            description=self.description_example,
            created_at=self.now_datetime.timestamp(),
            is_done=True,
            completed_at=self.end_date_example.timestamp(),
        )
        self.tasks_list_2.add_task(
            description=self.description_example,
            created_at=self.now_datetime.timestamp(),
        )

        self.tasks_list_4.add_task(
            description=self.description_example,
            created_at=self.now_datetime.timestamp(),
        )

        db.session.add(self.tasks_list_1)
        db.session.add(self.tasks_list_2)
        db.session.add(self.tasks_list_4)
        db.session.commit()

        self.test_description = "testing this description"
        self.test_is_done = False
